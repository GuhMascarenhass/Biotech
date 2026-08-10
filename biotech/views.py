import os
import io
import csv
import base64
import requests
from PIL import Image
from xhtml2pdf import pisa
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.files.base import ContentFile
from django.http import JsonResponse
from .models import AnaliseParasita
from ultralytics import YOLO 
from django.views.decorators.csrf import csrf_exempt
import json

# Carrega o modelo uma única vez
MODEL_PATH = os.path.join(settings.BASE_DIR, 'best.pt')
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"ERRO AO CARREGAR MODELO: {e}")
    model = None

DADOS_BACTERIAS = [
    {"nome": "Entamoeba", "color": "blue"},
    {"nome": "Giardia", "color": "green"},
    {"nome": "Cystoisospora", "color": "purple"},
    {"nome": "Toxocara", "color": "red"},
]

def analises(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    preview_dir = os.path.join(settings.MEDIA_ROOT, "preview")
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(preview_dir, exist_ok=True)
    
    fs_preview = FileSystemStorage(location=preview_dir)
    context = {
        "bacterias": DADOS_BACTERIAS,
        "images_preview": request.session.get('images_preview', []),
        "images_count": len(request.session.get('images_preview', []))
    }

    if request.method == "POST":
        action = request.POST.get('action')

        # 1. Upload para Preview
        if request.FILES.getlist("images") and not action:
            uploaded_files = request.FILES.getlist("images")
            preview_list = []
            for upload_file in uploaded_files[:10]:
                filename = fs_preview.save(upload_file.name, upload_file)
                preview_list.append({
                    "name": upload_file.name,
                    "url": settings.MEDIA_URL + "preview/" + filename,
                    "path": filename
                })
            request.session['images_preview'] = preview_list
            return redirect('analises')

        # 2. Analisar com IA e enviar para API
        elif action == 'analisar':
            if 'images_preview' in request.session and model:
                amostra_id = request.POST.get('amostra_id')
                for img_preview in request.session['images_preview']:
                    preview_path = os.path.join(preview_dir, img_preview['path'])
                    
                    if os.path.exists(preview_path):
                        results = model(preview_path, conf=0.25)
                        r = results[0]

                        deteccoes = r.boxes if (r.boxes is not None) else r.obb
                        label_ia, conf_val = "Negativo", 0
                        
                        if deteccoes and len(deteccoes) > 0:
                            label_ia = r.names[int(deteccoes.cls[0])]
                            conf_val = int(deteccoes.conf[0] * 100)

                        im_bgr = r.plot()
                        im_rgb = Image.fromarray(im_bgr[..., ::-1])
                        
                        buffer = io.BytesIO()
                        im_rgb.save(buffer, format="JPEG")
                        # Envia para a API
                    buffer.seek(0)
                    nome_final = f"res_{img_preview['path']}"
                    api_response = requests.post(
                        'http://127.0.0.1:8001/analise/',
                        data={
                            'parasita_detectado': label_ia,
                            'confianca': conf_val,
                            'status': 'CONCL',
                            'lamina' : amostra_id,
                        },
                        files={
                            'imagem': (nome_final, buffer, 'image/jpeg')
                        }
                    )

                    if api_response.status_code != 201:
                        print(f"Erro ao salvar na API: {api_response.json()}")
                        os.remove(preview_path)
                
                del request.session['images_preview']
                return redirect('dashboard_list')

        # 3. Limpar Preview
        elif action == 'limpar_preview':
            request.session['images_preview'] = []
            return redirect('analises')

    return render(request, "biotech/analises.html", context)
def dashboard_list(request):
    # Busca os dados da API
    api_response = requests.get('http://127.0.0.1:8001/analise/')
    dados = api_response.json()  # dados é uma lista de dicionários

    # Filtros (feitos em Python, não no banco)
    parasita = request.GET.get('parasita')
    data_inicio = request.GET.get('data_inicio')
    conf_min = request.GET.get('confianca')

    if parasita:
        dados = [d for d in dados if parasita.lower() in (d.get('parasita_detectado') or '').lower()]
    if data_inicio:
        dados = [d for d in dados if str(d.get('data_analise', '')).startswith(data_inicio)]
    if conf_min:
        dados = [d for d in dados if (d.get('confianca') or 0) >= float(conf_min)]

    # Exportação CSV
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="relatorio.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'ID Amostra', 'Paciente', 'Data', 'Parasita', 'Confiança (%)'])
        for item in dados:
            writer.writerow([
                item.get('id'),
                item.get('lamina'),
                item.get('paciente', 'Não Identificado'),
                item.get('data_analise'),
                item.get('parasita_detectado'),
                item.get('confianca'),
            ])
        return response

    # Exportação PDF
    if request.GET.get('export') == 'pdf':
        html = render_to_string('biotech/pdf_template.html', {'analises': dados})
        response = HttpResponse(content_type='application/pdf')
        pisa.CreatePDF(html, dest=response)
        return response

    return render(request, 'biotech/dashboard_list.html', {'resultados': dados})

@csrf_exempt
def salvar_amostra_sessao(request):
    if request.method == 'POST':
        dados = json.loads(request.body)
        request.session['ultima_amostra_id'] = dados.get('amostra_id')
        return JsonResponse({'ok': True})
    return JsonResponse({'erro': 'Método inválido'}, status=400)
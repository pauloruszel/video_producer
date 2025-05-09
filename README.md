# 🎥 Video Producer - Kafka Streamer

Este projeto captura frames de uma fonte de vídeo (webcam, vídeo local ou câmera ONVIF), codifica-os em base64 e os envia para um tópico Kafka.

## 📦 Tecnologias

- Python 3.12  
- OpenCV  
- Confluent Kafka (via `confluent-kafka`)  
- Docker + Docker Compose  
- Kafka UI (provectuslabs/kafka-ui)  
- ONVIF (opcional)  

## 🧱 Estrutura do Projeto

```text
video_producer/
├── config/
│   └── settings.py             # Configuração de broker Kafka, tópico e FPS
├── docker-compose.yml          # Ambiente Kafka + Kafka UI
├── kafka_client/
│   └── producer_service.py     # Lógica de captura e envio de frames para Kafka
├── models/
│   └── frame_message.py        # Estrutura JSON dos frames enviados
├── video/
│   ├── onvif_utils.py          # Integração com câmeras ONVIF (opcional)
│   └── source_factory.py       # Abstração da origem do vídeo (webcam, arquivo, ONVIF)
├── main.py                     # Ponto de entrada da aplicação
├── Dockerfile                  # Container Python
├── requirements.txt            # Dependências Python
├── start.ps1                   # Script PowerShell para iniciar projeto
└── reset_completo.ps1          # Script PowerShell para reset completo do ambiente
```



## 🚀 Execução

### 1. Pré-requisitos

- Docker + Docker Compose  
- Python 3.12  
- PowerShell (no Windows)

> 💡 **Dica (Linux):** pode ser necessário instalar dependências como `libgl1`:
>
> ```bash
> sudo apt-get install -y libgl1
> ```

### 2. Inicialização rápida (Windows)

```powershell
.\start.ps1
```

Esse script irá:

- Ativar o ambiente virtual  
- Instalar dependências  
- Subir containers Kafka  
- Iniciar a aplicação Python  

### 3. Reset completo

```powershell
.\reset_completo.ps1
```

Esse script irá:

- Derrubar e limpar volumes/redes Docker  
- Reinstalar dependências  
- Subir os containers e reiniciar a aplicação  

## 🧪 Tópicos Kafka

- `topic.frame.original`  
- `topic.frame.processado`  

Você pode visualizar os dados em **Kafka UI** acessando:  
[http://localhost:8080](http://localhost:8080)

## 🔧 Configurações

Você pode definir variáveis de ambiente diretamente ou via `.env`:

- `KAFKA_BROKER`: brokers Kafka (opcional, padrão: detecta automaticamente localhost ou container)  
- `USE_ONVIF`: ativa captura ONVIF (`true` ou `false`)  

Exemplo de configuração de câmera ONVIF:

```python
cap = open_video_source(source_type="auto", onvif_config={
    "ip": "192.168.1.101",
    "user": "admin",
    "password": "senha"
})
```

> O arquivo settings.py detecta automaticamente se o código está rodando em container e configura o broker conforme necessário.
Atenção: a câmera ONVIF deve estar na mesma rede que o host/container.

## 📤 Dados enviados para o Kafka

```json
{
  "frameId": "UUID",
  "cameraId": "CAM_FLEX",
  "sourceType": "webcam",
  "encoding": "jpeg",
  "timestamp": "2025-05-09T21:30:45.000Z",
  "frame": "base64string"
}
```

## 👁️ Visualização

Se `exibir_janela=True`, o frame será exibido localmente em uma janela usando `cv2.imshow()`.

## 🛠️ Build do container (manual)

```bash
docker build -t video-producer .
docker run --network=host video-producer
```

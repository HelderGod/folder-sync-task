# folder-sync-task

Este repositório contém um script Python para sincronização de pastas. O script sincroniza duas pastas (`source` e `replica`) de forma unidirecional, garantindo que o conteúdo da pasta `replica` seja uma cópia exata da pasta `source`.

## Pré requisitos

Antes de executar o script, será preciso configurar o ambiente. Siga os passos abaixo:

1. **Crie as Pastas:**
   - Crie uma pasta chamada `source`. Esta pasta será usada para armazenar os arquivos que serão sincronizados.
   - Crie uma pasta chamada `replica`. Esta pasta será a cópia exata da pasta `source`.
2. **Crie o Arquivo de Log:**
   - Crie um arquivo de texto chamado `log.txt` onde os logs das operações serão guardados.
3. **Preencha a Pasta Source:**
   - Adicione alguns arquivos (pode ser qualquer tipo de arquivo, como texto, imagem, etc.) à pasta `source`. O script irá sincronizar esses arquivos com a pasta `replica`.

## Como Executar o Script

Depois de configurar as pastas e o arquivo de log, o script pode ser executado da seguinte maneira:

```bash
python sync.py <caminho_para_a_pasta_source> <caminho_para_a_pasta_replica> <intervalo_de_sincronizacao_em_segundos> <caminho_do_arquivo_log>


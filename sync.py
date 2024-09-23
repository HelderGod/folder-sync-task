import os
import shutil
import time
import logging
import argparse
import signal
import sys

# Função para configurar o logging
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Função para sincronizar os arquivos e diretórios entre source e réplica
def sync_folders(source, replica):
    try:
        # Sincronizar a pasta source com a replica
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_path = os.path.join(replica, relative_path)

            # Criar diretórios que existem na source mas não na réplica
            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                logging.info(f'Diretório criado: {replica_path}')
                print(f'Diretório criado: {replica_path}')

            # Sincronizar arquivos
            for file_name in files:
                source_file = os.path.join(root, file_name)
                replica_file = os.path.join(replica_path, file_name)

                # Se o arquivo não existe ou foi modificado, copiar
                if not os.path.exists(replica_file) or os.path.getmtime(source_file) > os.path.getmtime(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f'Arquivo copiado/atualizado: {replica_file}')
                    print(f'Arquivo copiado/atualizado: {replica_file}')

        # Remover arquivos e diretórios que estão na réplica mas não na source
        for root, dirs, files in os.walk(replica, topdown=False):
            relative_path = os.path.relpath(root, replica)
            source_path = os.path.join(source, relative_path)

            # Remover arquivos que já não estão na source
            for file_name in files:
                replica_file = os.path.join(root, file_name)
                source_file = os.path.join(source_path, file_name)

                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.info(f'Arquivo removido: {replica_file}')
                    print(f'Arquivo removido: {replica_file}')

            # Remover diretórios vazios na réplica apenas se eles não existirem na source
            if not os.listdir(root) and not os.path.exists(source_path):
                os.rmdir(root)
                logging.info(f'Diretório removido: {root}')
                print(f'Diretório removido: {root}')

    except Exception as e:
        logging.error(f'Erro durante a sincronização: {e}')
        print(f'Erro durante a sincronização: {e}')

# Função para capturar sinais (Ctrl+C) e finalizar o programa de forma limpa
def signal_handler(sig, frame):
    print('Sincronização interrompida pelo utilizador.')
    sys.exit(0)

# Função principal para definir argumentos e iniciar a sincronização
def main():
    # Configurar a captura de interrupção (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Definir argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Sincronização de duas pastas")
    parser.add_argument("source", help="Caminho da pasta source")
    parser.add_argument("replica", help="Caminho da pasta replica")
    parser.add_argument("interval", type=int, help="Intervalo de sincronização (segundos)")
    parser.add_argument("log_file", help="Caminho do arquivo de log")

    args = parser.parse_args()

    # Validar os diretórios e intervalo
    if not os.path.exists(args.source):
        print(f"Erro: A pasta source '{args.source}' não existe.")
        sys.exit(1)
    if not os.path.exists(args.replica):
        print(f"Erro: A pasta replica '{args.replica}' não existe.")
        sys.exit(1)
    if args.interval <= 0:
        print("Erro: O intervalo de sincronização deve ser maior que 0 segundos.")
        sys.exit(1)

    # Configurar o sistema de logging
    setup_logging(args.log_file)

    # Loop de sincronização periódica
    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()

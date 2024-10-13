import shutil
import os
import datetime
import argparse
import curses
import sys

def realizar_backup(origem, destino):
    try:
        agora = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_dir = os.path.join(destino, agora)
        if os.path.exists(backup_dir):
            return False, f"Erro: O diretório de destino já existe: {backup_dir}"
        
        shutil.copytree(origem, backup_dir)
        
        return True, f"Backup concluído com sucesso em: {backup_dir}"
    except Exception as e:
        return False, f"Erro durante o backup: {str(e)}"

def main(stdscr):
    parser = argparse.ArgumentParser(description='Realiza backups periódicos')
    parser.add_argument('-o', '--origem', required=True, help='Diretório de origem dos arquivos')
    parser.add_argument('-d', '--destino', required=True, help='Diretório de destino dos backups')
    args = parser.parse_args()

    curses.curs_set(0)
    stdscr.clear()

    stdscr.addstr(0, 0, "Bem-vindo ao sistema de backup!", curses.A_BOLD)
    stdscr.addstr(2, 0, f"Diretório de origem: {args.origem}")
    stdscr.addstr(3, 0, f"Diretório de destino: {args.destino}")
    stdscr.addstr(5, 0, "Iniciando o backup...")
    stdscr.refresh()

    success, message = realizar_backup(args.origem, args.destino)

    if success:
        stdscr.addstr(7, 0, message, curses.A_BOLD)
    else:
        stdscr.addstr(7, 0, message, curses.A_BOLD | curses.A_REVERSE)

    stdscr.addstr(9, 0, "Pressione qualquer tecla para sair...")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(1)
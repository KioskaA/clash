import sys
import asyncio
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from qasync import QEventLoop, asyncSlot

from config import settings
from ui.ui import MainWindow
from cocapi import 



APILogin = settings.coc_api["login"]
APIPassword = settings.coc_api["password"]
Clantag = settings.coc_api["clantag"]


class ApplicationManager:
    def __init__(self):
        self.datagetter = None
        self.window = None

    @asyncSlot()
    async def startup(self):
        try:
            self.datagetter = DataGetter()
            await self.datagetter.login(APILogin, APIPassword)
            
            self.window = MainWindow()
            
            @asyncSlot(str)
            async def on_member_selected(membertag):
                try:
                    print(f"Выбран игрок с тегом {membertag}")
                    member_data = await self.datagetter.on_member_selected(membertag)
                    if member_data:
                        self.window.populate_player_frame(member_data)
                        self.window.populate_extra_frame(member_data)
                    else:
                        print(f"Игрок {membertag} не найден")
                except Exception as e:
                    print(f"Ошибка при получении данных игрока: {e}")
                    traceback.print_exc()
            
            self.window.member_selected.connect(on_member_selected)
            
            members = await self.datagetter.getClanMembers_byclantag(Clantag)
            mbrs_activity = create_activity_list(len(members))
            self.window.populate_members_table(members, mbrs_activity)
            
            self.window.show()
            
        except Exception as e:
            print(f"Ошибка при инициализации: {e}")
            traceback.print_exc()
            QTimer.singleShot(0, app.quit)

    async def shutdown(self):
        print("Завершение работы...")
        if self.datagetter:
            await self.datagetter.logout()


def main():
    global app
    app = QApplication(sys.argv)
    
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    manager = ApplicationManager()

    # Запускаем асинхронную инициализацию
    QTimer.singleShot(0, manager.startup)
    
    # Регистрируем cleanup при выходе
    app.aboutToQuit.connect(lambda: asyncio.ensure_future(manager.shutdown()))

    # Запускаем цикл событий Qt (он управляет asyncio)
    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
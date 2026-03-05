import coc
import asyncio
from temp.config import settings

APILogin = settings.coc_api["login"]
APIPassword = settings.coc_api["password"]
Clantag = settings.coc_api["clantag"]



class DataGetter():
    def __init__(self):
        self.client = None
        self.clan = None
        self._logged_in = False

    async def login(self, email, password):
        try:
            self.client = coc.Client(cache_max_size=0)
            await self.client.login(email, password)
            self._logged_in = True
            print(f"DataGetter.login(): success")
        except Exception as e:
            print(f"DataGetter.login(): error - {e}")
            raise

    async def logout(self):
        if self.client and self._logged_in:
            try:
                await self.client.close()
                self._logged_in = False
                print(f"DataGetter.logout(): logout")
            except Exception as e:
                print(f"DataGetter.logout(): error - {e}")



async def main():
    getter = None
    try:
        getter = DataGetter()
        await getter.login(APILogin, APIPassword)



        print("Тестовый запуск успешен")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        if getter:
            await getter.logout()

if __name__ == "__main__":
    asyncio.run(main())
import asyncio
import json
from typing import Self
from types import TracebackType

import httpx
import bs4

from models.schemas import RealEstateItem

class SrealityExtractor:
    """Asynchronní extraktor dat z portálu Sreality využívající skryté Next.js API."""
    BASE_URL: str = "https://www.sreality.cz"
    DEFAULT_HEADERS: Dict[str, str] = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "cs,cs-CZ;q=0.9,en;q=0.8",
    }
    def __init__(self) -> None:
        # Ukotvení stavu klienta do prázdnoty před jeho zrozením
        self._client: httpx.AsyncClient | None = None
        self._build_id: str = ""

    async def __aenter__(self) -> Self:
        """
        Iniciační fáze. Naváže spojení, získá dynamický klíč a vrátí instanci.
        """
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers=self.DEFAULT_HEADERS,
            timeout=httpx.Timeout(15.0)
        )

        await self._fetch_build_id()

        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        """
        Fáze rozpuštění. Garantovaný úklid energetického toku.
        """
        if self._client is not None:
            await self._client.aclose()


    async def _fetch_build_id(self) -> None:
        # Vyslání záměru a zastavení toku času pro tuto metodu
        response = await self._client.get("/")

        # Oživení mrtvé hmoty (Transformace stromu)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # 2. Izolace uzlu (Chirurgický řez)
        script_node = soup.find("script", id="__NEXT_DATA__")

        # Ochrana toku (Validace existence)
        if script_node is None:
            raise RuntimeError("Uzel s Build ID nebyl nalezen. Struktura Sreality se pravděpodobně změnila.")

        # Vytěžení esence (Zisk surového obsahu)
        raw_json_text = script_node.text

        try:
            # Překlad hmoty (Deserializace do Pythonu)
            data = json.loads(raw_json_text)

            # Cílová extrakce (Ukotvení klíče)
            self._build_id = data["bildId"]
        except (json.JSONDecodeError, KeyError) as e:
            # Překlad systémové entropie do kontrolované výjimky
            raise RuntimeError(f"Krystalizace datového klíče selhala: {e}")
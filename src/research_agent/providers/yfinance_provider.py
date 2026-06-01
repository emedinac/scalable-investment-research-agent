from research_agent.providers.base import MarketSnapshot


class YFinanceMarketDataProvider:
    async def snapshot(self, ticker: str) -> MarketSnapshot:
        import yfinance as yf

        ticker = ticker.upper().replace(" ", "")
        info = yf.Ticker(ticker).fast_info
        price = float(info.get("last_price") or info.get("lastPrice") or 0.0)
        return MarketSnapshot(
            ticker=ticker,
            current_price=price,
            eps=None,
            revenue_growth_yoy=None,
            operating_margin=None,
        )

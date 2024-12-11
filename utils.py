class Symbol:
    """Represents a trading symbol with a base and quote currency."""

    def __init__(self, base: str, quote: str) -> None:
        """
        Initialize a Symbol object.

        Args:
            base (str): Base currency.
            quote (str): Quote currency.
        """
        self.base = base
        self.quote = quote


class ShortTicker:
    """Represents a trading ticker with last price and optional reversal."""

    def __init__(self, symbol: Symbol, last_price: float, reversed: bool = False) -> None:
        """
        Initialize a ShortTicker object.

        Args:
            symbol (Symbol): Trading symbol for the ticker.
            last_price (float): Last trade price for the ticker.
            reversed (bool): Indicates if the ticker is reversed. Defaults to False.
        """
        self.symbol = symbol
        self.last_price = last_price
        self.reversed = reversed

    def __repr__(self) -> str:
        """
        Represent the ticker as a string.

        Returns:
            str: String representation of the ticker.
        """
        direction = f"{self.symbol.base}/{self.symbol.quote}"
        if self.reversed:
            direction += " (Reversed)"
        return f"{direction} @ {self.last_price}"
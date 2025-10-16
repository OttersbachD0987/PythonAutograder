from typing import Self, NamedTuple, overload, Iterator

class Version(NamedTuple):
    """_summary_
    
    _description_
    """
    major: int
    minor: int
    patch: int
    build: int
    
    @staticmethod
    def init(a_versionString: str) -> Self:
        """_summary_

        Args:
            a_versionString (str): _description_
        """
        info: map[int] = map(int, a_versionString.split("."))
        return Version(next(info), next(info), next(info), next(info))
    
    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"{self.major:0>4}.{self.minor:0>4}.{self.patch:0>4}.{self.build:0>4}"
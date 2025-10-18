from typing import NamedTuple

class Version(NamedTuple):
    """_summary_
    
    _description_
    """
    major: int
    minor: int
    patch: int
    build: int
    
    @staticmethod
    def init(a_versionString: str) -> "Version":
        """_summary_

        Args:
            a_versionString (str): _description_
        """
        return Version(next(info := map(int, a_versionString.split("."))), next(info), next(info), next(info))
    
    def __repr__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        return f"{self.major:0>4}.{self.minor:0>4}.{self.patch:0>4}.{self.build:0>4}"
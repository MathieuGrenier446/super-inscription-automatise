class Course:
    def __init__(self, sigle: str, lab_group: int, theo_group: int) -> None:
        self.sigle = sigle
        self.lab_group = lab_group
        self.theo_group = theo_group

    def __repr__(self) -> str:
        return f"Course({self.sigle}, {self.lab_group}, {self.theo_group})"
    
    def __eq__(self, other):
        if isinstance(other, Course):
            return (self.sigle == other.sigle)
        return False
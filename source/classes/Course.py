class Course:
    def __init__(self, sigle: str, lab_groups: list[int] | int, theo_groups: list[int] | int) -> None:
        if isinstance(lab_groups, int):
            lab_groups = [lab_groups]
        if isinstance(theo_groups, int):
            theo_groups = [theo_groups]
        self.sigle = sigle
        self.lab_groups = lab_groups
        self.theo_groups = theo_groups

    def __repr__(self) -> str:
        return f"Course({self.sigle}, {self.lab_groups}, {self.theo_groups})"
    
    def __eq__(self, other):
        if isinstance(other, Course):
            return (self.sigle == other.sigle 
                    and self.lab_groups == other.lab_groups 
                    and self.theo_groups == other.theo_groups)
        return False
class UserCreate(BaseModel):
    """Schema for creating a new user.

    This schema defines the required fields for creating a new user, including username, email, password, and optionally a role.
    """

    username: str
    email: EmailStr
    password: str | None = None
    role: Optional[RoleEnum] = RoleEnum.user


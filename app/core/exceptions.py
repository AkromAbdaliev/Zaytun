from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
)
UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)
CategoryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
)

CategoryAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Category already exists"
)

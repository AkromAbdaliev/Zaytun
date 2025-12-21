from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
)


UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
)

CategoryNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
)

CategoryAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Category already exists"
)
ListingNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found"
)

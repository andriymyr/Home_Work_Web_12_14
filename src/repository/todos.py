from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Todo, User
from src.schemas.todo import TodoSchema, TodoUpdateSchema


async def get_todos(limit: int, offset: int, db: AsyncSession, user: User):
    """
    Get a list of todos for the specified user.

    :param limit: int: Limit the number of todos returned.
    :param offset: int: Skip the first n results.
    :param db: AsyncSession: Database connection to use.
    :param user: User: User object to filter todos.
    :return: List of todo objects.
    :doc-author: 
    """    
    stmt = select(Todo).filter_by(user=user).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_all_todos(limit: int, offset: int, db: AsyncSession):
    """
    Get a list of all todos in the database.

    :param limit: int: Limit the number of todos returned.
    :param offset: int: Specify how many rows to skip.
    :param db: AsyncSession: Database connection to use.
    :return: List of todo objects.
    :doc-author: 
    """    
    stmt = select(Todo).offset(offset).limit(limit)
    todos = await db.execute(stmt)
    return todos.scalars().all()


async def get_todo(todo_id: int, db: AsyncSession, user: User):
    """
    Get a todo by its ID for the specified user.

    :param todo_id: int: ID of the todo to retrieve.
    :param db: AsyncSession: Database connection to use.
    :param user: User: User object for filtering todos.
    :return: Todo object or None if not found.
    """   
    stmt = select(Todo).filter_by(id=todo_id, user=user)
    todo = await db.execute(stmt)
    return todo.scalar_one_or_none()


async def create_todo(body: TodoSchema, db: AsyncSession, user: User):
    """
    Create a new todo.

    :param body: TodoSchema: Todo data to create.
    :param db: AsyncSession: Database connection to use.
    :param user: User: User object for associating with the todo.
    :return: Created Todo object.
    """    
    todo = Todo(
        **body.model_dump(exclude_unset=True), user=user
    )  # (title=body.title, description=body.description)
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


async def update_todo(
    todo_id: int, body: TodoUpdateSchema, db: AsyncSession, user: User
):
    """
    Update an existing todo.

    :param todo_id: int: ID of the todo to update.
    :param body: TodoUpdateSchema: Updated todo data.
    :param db: AsyncSession: Database connection to use.
    :param user: User: User object for security check.
    :return: Updated Todo object or None if not found.
    """    
    stmt = select(Todo).filter_by(id=todo_id, user=user)
    result = await db.execute(stmt)
    todo = result.scalar_one_or_none()
    if todo:
        todo.title = body.title
        todo.description = body.description
        todo.completed = body.completed
        await db.commit()
        await db.refresh(todo)
    return todo


async def delete_todo(todo_id: int, db: AsyncSession, user: User):
    """
    Delete a todo by ID.

    :param todo_id: int: ID of the todo to delete.
    :param db: AsyncSession: Database connection to use.
    :param user: User: User object for security check.
    :return: Deleted Todo object or None if not found.
    """    
    stmt = select(Todo).filter_by(id=todo_id, user=user)
    todo = await db.execute(stmt)
    todo = todo.scalar_one_or_none()
    if todo:
        await db.delete(todo)
        await db.commit()
    return todo

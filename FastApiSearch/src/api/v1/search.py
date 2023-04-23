from fastapi import APIRouter, Depends, status, Response, Query

from services.post import PostService, get_post_service
from .schemas import Post


router = APIRouter()


@router.get(
    '/search',
    description='find all posts that match the query',
    summary='find posts by query',
    status_code=status.HTTP_200_OK,
    response_model=list[Post]
)
async def find_posts(query: str | None = Query(default=None), post_service: PostService = Depends(get_post_service)):
    resp = await post_service.search_posts(query)
    result = [Post.parse_obj(p[0].__dict__) for p in resp]
    return result


@router.delete(
    '/{post_id}',
    description='delete post by id',
    summary='delete post by id',
    status_code=status.HTTP_202_ACCEPTED
)
async def delete_post(post_id: str, post_service: PostService = Depends(get_post_service)):
    resp = await post_service.delete_post(post_id)
    print(resp)
    if resp:
        return Response(status_code=status.HTTP_202_ACCEPTED)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

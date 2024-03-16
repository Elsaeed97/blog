from rest_framework import viewsets, status, permissions
from .serializers import PostSerializer
from .models import Post
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get("title")
        if len(title) > 200:
            return Response(
                {"title": "Title must be less than 200 characters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == request.user:
            return super().update(request, *args, **kwargs)
        else:
            return Response(
                {"message": "You are not allowed to update this post"}, status=403
            )

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author == request.user:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(
                {"message": "You are not allowed to delete this post"}, status=403
            )

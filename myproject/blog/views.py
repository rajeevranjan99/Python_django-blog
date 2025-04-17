from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer

# ✅ List all posts
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# ✅ Create a new post with dynamic field selection
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        requested_fields = request.query_params.get("fields", "").split(",") or None
        serializer = self.get_serializer(data=request.data, fields=requested_fields)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ✅ Retrieve, Update, or Delete a post with existence check
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_object(self):
        """Retrieve the post object or return 404"""
        return super().get_object()

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        requested_fields = request.query_params.get("fields", "").split(",") or None
        serializer = self.get_serializer(post, data=request.data, partial=True, fields=requested_fields)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        self.perform_destroy(post)
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

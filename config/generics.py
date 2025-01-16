from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status


class RetrieveInListAPI(ListAPIView):
    
    def get_queryset(self): 
        pk = self.kwargs.get('pk')
        if pk is not None:
            return self.queryset.filter(pk=pk)
        return self.queryset.none()  # Возвращаем пустой queryset, если pk не указан

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'Object not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
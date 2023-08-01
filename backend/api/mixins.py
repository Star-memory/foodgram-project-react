from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404


class ListRetriveSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    pass


class CreateListRetriveSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    pass


class CreateDestroyMixin:

    def create_сustom(self, request, model, serializer, obj_field,
                      obj_id_field, obj, obj_id, error_message):
        if model.objects.filter(
                **{obj_field: obj, obj_id_field: obj_id}).exists():
            return Response({'error': error_message},
                            status=status.HTTP_400_BAD_REQUEST)
        obj_create = model.objects.create(
            **{obj_field: obj, obj_id_field: obj_id})
        serializer = serializer(obj_create, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy_сustom(self, request, model, obj_field, obj_id_field, obj,
                       obj_id, detail_message):
        if request.method == 'DELETE':
            get_object_or_404(
                model, **{obj_field: obj, obj_id_field: obj_id}).delete()
            return Response({'detail': detail_message},
                            status=status.HTTP_204_NO_CONTENT)

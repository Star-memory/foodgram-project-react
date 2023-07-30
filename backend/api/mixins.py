from rest_framework import mixins, viewsets


class ListRetriveSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    pass


class CreateListRetriveSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    pass

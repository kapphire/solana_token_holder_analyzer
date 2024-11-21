from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework.response import Response
from rest_framework import status
from addresses.handlers import SolanaTokenAnalyzer

from rest_framework import generics

# Create your views here.
class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def create(self, request, *args, **kwargs):
        # Custom logic before saving
        data = request.data
        token_analyzer = SolanaTokenAnalyzer(data.get('address'))
        token_data = token_analyzer.update_holder_data()

        # Use the serializer to validate the data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save the object
        if token_data:
            self.perform_create(serializer)

        # Custom logic after saving
        # response_data = serializer.data
        response_data = token_data

        # Return a custom response
        return Response(response_data, status=status.HTTP_201_CREATED)

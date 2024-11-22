from addresses.models import Address
from addresses.serializers import AddressSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from addresses.handlers import SolanaTokenAnalyzer

from rest_framework import generics

# Create your views here.
class AddressList(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        address = data.get('address')

        # Proceed with your custom logic
        token_analyzer = SolanaTokenAnalyzer(address)
        token_data = token_analyzer.update_holder_data()

        # Validate and save the object
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        if token_data:
            if not Address.objects.filter(address=address).exists():
                self.perform_create(serializer)

        # Return custom response
        response_data = token_data
        return Response(response_data, status=status.HTTP_201_CREATED)

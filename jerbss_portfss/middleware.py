class ContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Set the correct content type for static files based on extension
        path = request.path.lower()
        if path.endswith('.css'):
            response['Content-Type'] = 'text/css'
        elif path.endswith('.js'):
            response['Content-Type'] = 'application/javascript'
        elif path.endswith('.jpg') or path.endswith('.jpeg'):
            response['Content-Type'] = 'image/jpeg'
        elif path.endswith('.png'):
            response['Content-Type'] = 'image/png'
        elif path.endswith('.gif'):
            response['Content-Type'] = 'image/gif'
            
        return response

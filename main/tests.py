from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, Tag
from .forms import ProjectForm
from datetime import date
import os

class ProjectModelTests(TestCase):
    def setUp(self):
        """Configuração inicial para os testes"""
        # Criar um usuário admin para testes
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Criar algumas tags
        self.tag1 = Tag.objects.create(name='Python')
        self.tag2 = Tag.objects.create(name='Django')
        
        # Criar um projeto de teste
        self.project = Project.objects.create(
            title='Projeto Teste',
            short_description='Descrição curta do projeto teste',
            content='Conteúdo detalhado do projeto teste',
            status='in_progress',
            project_type='web',
            start_date=date.today()
        )
        self.project.tags.add(self.tag1, self.tag2)

    def test_project_creation(self):
        """Testa se um projeto é criado corretamente"""
        self.assertEqual(self.project.title, 'Projeto Teste')
        self.assertEqual(self.project.status, 'in_progress')
        self.assertEqual(self.project.tags.count(), 2)

    def test_project_str_representation(self):
        """Testa a representação string do projeto"""
        self.assertEqual(str(self.project), 'Projeto Teste')

    def test_slug_generation(self):
        """Testa se o slug é gerado corretamente"""
        self.assertTrue(self.project.slug)
        self.assertIn('projeto-teste', self.project.slug)

    def test_get_status_display_html(self):
        """Testa o método get_status_display_html"""
        html = self.project.get_status_display_html
        self.assertIn('badge bg-warning text-dark', html)
        self.assertIn('Em andamento', html)

class ProjectViewTests(TestCase):
    def setUp(self):
        """Configuração inicial para os testes de views"""
        self.client = Client()
        # Create test image file
        image_path = os.path.join(os.path.dirname(__file__), 'static', 'img', 'default-project.jpg')
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(image_path, 'rb').read() if os.path.exists(image_path) else b'',
            content_type='image/jpeg'
        )
        
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        # Create test project
        self.project = Project.objects.create(
            title='Projeto Teste',
            short_description='Descrição curta',
            content='Conteúdo detalhado',
            status='in_progress',
            project_type='web',
            image=self.image
        )

    def test_create_project_view_unauthorized(self):
        """Testa tentativa de criar projeto sem autorização"""
        response = self.client.get(reverse('main:create_project'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_create_project_view_authorized(self):
        """Testa criação de projeto como admin"""
        # Login as admin
        self.client.login(username='admin', password='adminpass123')
        
        # Get create project page
        response = self.client.get(reverse('main:create_project'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/create_project.html')
        self.assertIsInstance(response.context['form'], ProjectForm)
        
        # Test form in context
        form = response.context['form']
        self.assertTrue('title' in form.fields)
        self.assertTrue('content' in form.fields)
        self.assertTrue('image' in form.fields)

    def test_projects_list_view(self):
        """Testa a view de listagem de projetos"""
        response = self.client.get(reverse('main:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/projects.html')
        self.assertContains(response, self.project.title)

    def test_project_detail_view(self):
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('main/static/img/profile_photo.png', 'rb').read(),
            content_type='image/jpeg'
        )

    def test_valid_form(self):
        """Testa se o formulário é válido com dados corretos"""
        form_data = {
            'title': 'Novo Projeto',
            'short_description': 'Descrição curta',
            'content': 'Conteúdo detalhado',
            'status': 'in_progress',
            'project_type': 'web',
            'tags_input': 'Python, Django',
            'start_date': date.today()
        }
        form = ProjectForm(data=form_data, files={'image': self.image})
        if not form.is_valid():
            print(form.errors)  # Debug form errors
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Testa se o formulário é inválido com dados incompletos"""
        form_data = {
            'title': '',  # título em branco deve invalidar o form
            'short_description': 'Descrição curta'
        }
        form = ProjectForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

class TagModelTests(TestCase):
    def test_tag_creation(self):
        """Testa a criação de tags"""
        tag = Tag.objects.create(name='Python')
        self.assertEqual(str(tag), 'Python')
        self.assertEqual(Tag.objects.count(), 1)

class IntegrationTests(TestCase):
    def setUp(self):
        """Configuração para testes de integração"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        # Create a proper test image
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('main/static/img/profile_photo.png', 'rb').read(),
            content_type='image/jpeg'
        )

    def test_project_creation_flow(self):
        """Testa o fluxo completo de criação de projeto"""
        self.client.login(username='admin', password='adminpass123')
        
        # Create form data with all required fields
        form_data = {
            'title': 'Projeto Integração',
            'short_description': 'Teste de integração',
            'content': 'Conteúdo do teste',
            'status': 'in_progress',
            'project_type': 'web',
            'tags_input': 'Python, Django, Test',
            'image': self.image
        }
        
        # Make the POST request
        response = self.client.post(
            reverse('main:create_project'),
            form_data,
            format='multipart'
        )
        
        # Debug output if project wasn't created
        if Project.objects.count() == 0:
            print("Form errors:", response.context['form'].errors if hasattr(response, 'context') else "No form in context")
        
        # Verify project creation
        self.assertEqual(Project.objects.count(), 1)
        project = Project.objects.first()
        self.assertEqual(project.title, 'Projeto Integração')
        self.assertEqual(project.tags.count(), 3)
        
        # Verificar redirecionamento
        self.assertRedirects(
            response,
            reverse('main:project_detail', kwargs={'slug': project.slug})
        )

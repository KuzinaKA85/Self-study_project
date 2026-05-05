from django.test import RequestFactory, TestCase

from materials.models import Course
from users.models import User
from users.permissions import IsAdmin, IsOwner, IsOwnerOrAdmin, IsStudentOrReadOnly, IsTeacher


class PermissionsTest(TestCase):
    """Тесты прав доступа."""

    def setUp(self):
        self.factory = RequestFactory()

        # Создаём админа
        self.admin = User(email="admin@test.com", role="admin")
        self.admin.set_password("123")
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()

        # Создаём учителя
        self.teacher = User(email="teacher@test.com", role="teacher")
        self.teacher.set_password("123")
        self.teacher.save()

        # Создаём студента
        self.student = User(email="student@test.com", role="student")
        self.student.set_password("123")
        self.student.save()

        # Курс принадлежит учителю
        self.course = Course.objects.create(title_course="Курс", description="Описание", owner=self.teacher)

    def _make_request(self, user):
        """Создаёт request с указанным пользователем."""

        request = self.factory.get("/")
        request.user = user
        return request

    # IsTeacher
    def test_teacher_has_teacher_rights(self):
        """Тест: Учитель имеет права учителя."""

        request = self._make_request(self.teacher)
        self.assertTrue(IsTeacher().has_permission(request, None))

    def test_student_has_not_teacher_rights(self):
        """Тест: Студент не имеет прав учителя."""

        request = self._make_request(self.student)
        self.assertFalse(IsTeacher().has_permission(request, None))

    # IsAdmin
    def test_admin_has_admin_rights(self):
        """Тест: Админ имеет права админа."""

        request = self._make_request(self.admin)
        self.assertTrue(IsAdmin().has_permission(request, None))

    def test_teacher_has_not_admin_rights(self):
        """Тест: Учитель не имеет прав админа."""

        request = self._make_request(self.teacher)
        self.assertFalse(IsAdmin().has_permission(request, None))

    # IsOwner
    def test_owner_can_edit(self):
        """Тест: Владелец может редактировать свой курс."""

        request = self._make_request(self.teacher)
        perm = IsOwner()
        self.assertTrue(perm.has_object_permission(request, None, self.course))

    def test_other_cannot_edit(self):
        """Тест: Другой не может редактировать чужой курс."""

        request = self._make_request(self.student)
        perm = IsOwner()
        self.assertFalse(perm.has_object_permission(request, None, self.course))

    # IsOwnerOrAdmin
    def test_admin_can_edit_any(self):
        """Тест: Админ может редактировать любой курс."""

        request = self._make_request(self.admin)
        perm = IsOwnerOrAdmin()
        self.assertTrue(perm.has_object_permission(request, None, self.course))

    def test_owner_can_edit_own(self):
        """Тест: Владелец может редактировать свой курс."""

        request = self._make_request(self.teacher)
        perm = IsOwnerOrAdmin()
        self.assertTrue(perm.has_object_permission(request, None, self.course))

    def test_other_cannot_edit_foreign(self):
        """Тест: Другой пользователь (не владелец/не админ) не может редактировать чужой курс."""

        request = self._make_request(self.student)
        perm = IsOwnerOrAdmin()
        self.assertFalse(perm.has_object_permission(request, None, self.course))

    def test_student_can_read_only(self):
        """Тест: Студент может только читать (GET), но не писать (POST)."""

        # GET запрос - студент может читать
        get_request = self.factory.get("/")
        get_request.user = self.student
        perm = IsStudentOrReadOnly()
        self.assertTrue(perm.has_permission(get_request, None))

        # POST запрос - студент не может писать
        post_request = self.factory.post("/")
        post_request.user = self.student
        self.assertFalse(perm.has_permission(post_request, None))

        # POST запрос от учителя - может писать
        post_request_teacher = self.factory.post("/")
        post_request_teacher.user = self.teacher
        self.assertTrue(perm.has_permission(post_request_teacher, None))

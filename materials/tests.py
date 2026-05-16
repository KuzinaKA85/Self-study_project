from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Section, Test, TestAttempt
from users.models import User


class CourseTestCase(APITestCase):
    """Тесты для модели курса"""

    def setUp(self):
        """Подготовка перед каждым тестом."""

        self.user = User.objects.create(email="test@example.com", password="testpass123", role="teacher")
        self.course = Course.objects.create(
            title_course="География",
            description="Описание курса 'География'",
            owner=self.user,
        )
        self.section = Section.objects.create(
            title_section="Первый раздел: 'Страны мира'",
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_list(self):
        """Тест: Получение списка курсов."""

        url = reverse("materials:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_retrieve(self):
        """Тест: Просмотр одного курса."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_course"),
            self.course.title_course,
        )

    def test_course_create(self):
        """Тест: Создание курса."""

        url = reverse("materials:course-list")
        data = {
            "title_course": "История",
            "description": "Описание курса 'История'",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тест: Обновление курса."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "title_course": "География. Дополнение № 1",
            "description": "Описание курса 'География'",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_course"),
            "География. Дополнение № 1",
        )

    def test_course_delete(self):
        """Тест: Удаление курса."""

        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Course.objects.all().count(), 0)


class SectionTestCase(APITestCase):
    """Тесты для модели раздела."""

    def setUp(self):
        """Подготовка перед каждым тестом."""

        self.user = User.objects.create(email="test@example.com", password="testpass123", role="teacher")
        self.course = Course.objects.create(
            title_course="География",
            description="Описание курса 'География'",
            owner=self.user,
        )
        self.section = Section.objects.create(
            title_section="Первый раздел: 'Страны мира'", course=self.course, order=1
        )
        self.client.force_authenticate(user=self.user)

    def test_section_list(self):
        """Тест: Список разделов."""

        url = reverse("materials:section-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_section_retrieve(self):
        """Тест: Просмотр одного раздела."""

        url = reverse("materials:section-detail", args=(self.section.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_section"),
            self.section.title_section,
        )

    def test_section_create(self):
        """Тест: Создание раздела."""

        url = reverse("materials:section-create")
        data = {"course": self.course.pk, "title_section": "Второй раздел: 'Города'", "order": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.all().count(), 2)

    def test_section_update(self):
        """Тест: Обновление раздела."""

        url = reverse("materials:section-update", args=(self.section.pk,))
        data = {
            "title_section": "Первый раздел: 'Страны мира'. Дополнение № 1",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_section"),
            "Первый раздел: 'Страны мира'. Дополнение № 1",
        )

    def test_section_delete(self):
        """Тест: Удаление раздела."""

        url = reverse("materials:section-delete", args=(self.section.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Section.objects.all().count(), 0)


class LessonTestCase(APITestCase):
    """Тесты для модели урока."""

    def setUp(self):
        """Подготовка пред каждым тестом."""

        self.user = User.objects.create(email="test@example.com", password="testpass123", role="teacher")
        self.course = Course.objects.create(
            title_course="География",
            description="Описание курса 'География'",
            owner=self.user,
        )
        self.section = Section.objects.create(
            title_section="Первый раздел: 'Страны мира'", course=self.course, order=1
        )
        self.lesson = Lesson.objects.create(
            title_lesson="Урок № 1 - Российская Федерация",
            description="Описание урока № 1",
            section=self.section,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        """Тест: Список уроков."""

        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_retrieve(self):
        """Тест: Просмотр одного урока."""

        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("title_lesson"),
            self.lesson.title_lesson,
        )

    def test_lesson_create(self):
        """Тест: Создание урока."""

        url = reverse("materials:lesson-create")
        data = {
            "section": self.section.id,
            "title_lesson": "Урок № 2 - Китайская Народная Республика",
            "description": "Описание урока № 2",
            "video_url": "https://www.youtube.com/watch?v=test",
            "order": 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        """Тест: Обновление урока."""

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title_lesson": "Урок № 2 - Китайская Народная Республика. Дополнение № 1",
            "description": "Описание урока № 2",
            "video_url": "https://www.youtube.com/watch?v=test",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title_lesson"), "Урок № 2 - Китайская Народная Республика. Дополнение № 1")

    def test_lesson_delete(self):
        """Тест: Удаление урока."""

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAPITestCase(APITestCase):
    """Тесты для проверки ответов на тесты."""

    def setUp(self):
        """Подготовка перед каждым тестом."""

        # Создаём учителя и студента
        self.teacher = User.objects.create(email="teacher@test.com", password="testpass123", role="teacher")
        self.student = User.objects.create(email="student@test.com", password="testpass123", role="student")

        # Создаём курс, раздел и урок
        self.course = Course.objects.create(title_course="География", description="Описание курса", owner=self.teacher)
        self.section = Section.objects.create(title_section="Страны мира", course=self.course, order=1)
        self.lesson = Lesson.objects.create(
            title_lesson="Столицы мира", description="Описание урока", section=self.section, owner=self.teacher
        )

        # Создаём тест для урока
        self.test = Test.objects.create(lesson=self.lesson, question="Столица России?", correct_answer="Москва")

        self.check_url = "/materials/check-test/"

    def test_check_correct_answer(self):
        """Тест: Правильный ответ."""

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.check_url, {"test_id": self.test.id, "answer": "Москва"})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["correct"])
        self.assertEqual(response.data["message"], "Правильно!")

        # Проверяем, что попытка сохранилась
        self.assertEqual(TestAttempt.objects.count(), 1)
        attempt = TestAttempt.objects.first()
        self.assertTrue(attempt.is_correct)

    def test_check_wrong_answer(self):
        """Тест: Неправильный ответ."""

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.check_url, {"test_id": self.test.id, "answer": "Санкт-петербург"})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["correct"])
        self.assertEqual(response.data["message"], "Неправильно")

        # Проверяем, что попытка сохранилась
        attempt = TestAttempt.objects.first()
        self.assertFalse(attempt.is_correct)

    def test_check_without_auth(self):
        """Тест: Неавторизованный пользователь не может пройти тест."""

        self.client.force_authenticate(user=None)

        response = self.client.post(self.check_url, {"test_id": self.test.id, "answer": "Москва"})

        self.assertEqual(response.status_code, 401)

    def test_check_test_not_found(self):
        """Тест: Тест не найден."""

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.check_url, {"test_id": 999, "answer": "Москва"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Тест не найден")

    def test_check_lesson_without_test(self):
        """Тест: У урока нет теста."""

        # Создаём урок без теста
        lesson_without_test = Lesson.objects.create(
            title_lesson="Урок без теста", description="Описание", section=self.section, owner=self.teacher
        )

        self.client.force_authenticate(user=self.student)

        response = self.client.post(self.check_url, {"test_id": lesson_without_test.id, "answer": "Москва"})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Тест не найден")


class TestAttemptModelTest(TestCase):
    """Тесты для модели TestAttempt (автоматическая проверка ответа)."""

    def setUp(self):
        self.teacher = User.objects.create(email="teacher@test.com", password="123", role="teacher")
        self.student = User.objects.create(email="student@test.com", password="123", role="student")

        self.course = Course.objects.create(title_course="Курс", description="Описание", owner=self.teacher)
        self.section = Section.objects.create(title_section="Раздел", course=self.course)
        self.lesson = Lesson.objects.create(
            title_lesson="Урок", description="Описание", section=self.section, owner=self.teacher
        )
        self.test = Test.objects.create(lesson=self.lesson, question="Вопрос?", correct_answer="Правильный ответ")

    def test_save_automatically_checks_answer(self):
        """Тест: При сохранении TestAttempt автоматически проверяется is_correct."""

        attempt = TestAttempt.objects.create(student=self.student, test=self.test, user_answer="Правильный ответ")

        self.assertTrue(attempt.is_correct)

        attempt2 = TestAttempt.objects.create(student=self.student, test=self.test, user_answer="Неправильный ответ")

        self.assertFalse(attempt2.is_correct)

    def test_save_ignores_case_and_spaces(self):
        """Тест: Проверка игнорирует регистр и пробелы."""

        attempt = TestAttempt.objects.create(student=self.student, test=self.test, user_answer="  ПРАВИЛЬНЫЙ ОТВЕТ  ")

        self.assertTrue(attempt.is_correct)


class TestCRUDAPITestCase(APITestCase):
    """Тесты для CRUD операций с тестами."""

    def setUp(self):
        # Учитель (владелец)
        self.teacher = User.objects.create(email="teacher@test.com", password="123", role="teacher")

        # Другой учитель (не владелец)
        self.other = User.objects.create(email="other@test.com", password="123", role="teacher")

        # Админ
        self.admin = User.objects.create(email="admin@test.com", password="123", role="admin")
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()

        # Курс и урок
        self.course = Course.objects.create(title_course="География", description="Описание", owner=self.teacher)
        self.section = Section.objects.create(title_section="Страны мира", course=self.course)
        self.lesson = Lesson.objects.create(
            title_lesson="Столицы", description="Описание", section=self.section, owner=self.teacher
        )

        # Второй урок для теста списка
        self.lesson2 = Lesson.objects.create(
            title_lesson="Реки", description="Описание", section=self.section, owner=self.teacher
        )

    def test_owner_can_create_test(self):
        """Владелец может создать тест."""

        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(
            "/materials/tests/", {"lesson": self.lesson.id, "question": "Столица Франции?", "correct_answer": "Париж"}
        )
        self.assertEqual(response.status_code, 201)

    def test_admin_can_create_test(self):
        """Админ может создать тест."""

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            "/materials/tests/", {"lesson": self.lesson.id, "question": "Вопрос", "correct_answer": "Ответ"}
        )
        self.assertEqual(response.status_code, 201)

    def test_other_cannot_create_test(self):
        """Другой учитель не может создать тест."""

        self.client.force_authenticate(user=self.other)
        response = self.client.post(
            "/materials/tests/", {"lesson": self.lesson.id, "question": "Вопрос", "correct_answer": "Ответ"}
        )
        self.assertEqual(response.status_code, 403)

    def test_owner_can_update_test(self):
        """Владелец может обновить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Старый", correct_answer="Ответ")
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(f"/materials/tests/{test.id}/", {"question": "Новый"})
        self.assertEqual(response.status_code, 200)

    def test_admin_can_update_test(self):
        """Админ может обновить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Старый", correct_answer="Ответ")
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(f"/materials/tests/{test.id}/", {"question": "Новый от админа"})
        self.assertEqual(response.status_code, 200)

    def test_other_cannot_update_test(self):
        """Другой учитель не может обновить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Старый", correct_answer="Ответ")
        self.client.force_authenticate(user=self.other)
        response = self.client.patch(f"/materials/tests/{test.id}/", {"question": "Новый"})
        self.assertEqual(response.status_code, 403)

    def test_owner_can_delete_test(self):
        """Владелец может удалить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Вопрос", correct_answer="Ответ")
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(f"/materials/tests/{test.id}/")
        self.assertEqual(response.status_code, 204)

    def test_admin_can_delete_test(self):
        """Админ может удалить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Вопрос", correct_answer="Ответ")
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f"/materials/tests/{test.id}/")
        self.assertEqual(response.status_code, 204)

    def test_other_cannot_delete_test(self):
        """Другой учитель не может удалить тест."""

        test = Test.objects.create(lesson=self.lesson, question="Вопрос", correct_answer="Ответ")
        self.client.force_authenticate(user=self.other)
        response = self.client.delete(f"/materials/tests/{test.id}/")
        self.assertEqual(response.status_code, 403)

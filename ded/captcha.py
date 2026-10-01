import base64
import io
import os
import random
import string
from typing import Optional

from PIL import Image, ImageDraw


class PuzzleCaptcha:
    """
    Генератор пазл-капчи.

    ТЗ.md: Пользователь должен собрать изображение из фрагментов.
    После сборки система проверяет правильность расположения.
    """

    def __init__(self, image_dir: Optional[str] = None, mode: str = "pieces"):
        self.challenges: dict[str, dict] = {}

        if image_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            image_dir = os.path.join(base_dir, "image")

        self.image_dir = image_dir
        self.image_files = self._load_image_files()
        self.mode = mode

    def _load_image_files(self) -> list[str]:
        """Загружает список файлов изображений из директории."""
        if not os.path.exists(self.image_dir):
            return []

        supported_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
        files = []
        for f in os.listdir(self.image_dir):
            ext = os.path.splitext(f)[1].lower()
            if ext in supported_extensions:
                files.append(f)
        return sorted(files)

    def generate(self, image_filename: Optional[str] = None) -> dict:
        """
        Генерирует пазл-капчу.

        Returns:
            dict с полями:
            - token: уникальный токен
            - fragments: список base64 изображений (в перемешанном порядке)
        """
        token = self._generate_token()

        if self.mode == "pieces":
            return self._generate_pieces_mode(token)
        else:
            return self._generate_grid_mode(token, image_filename)

    def _generate_token(self) -> str:
        """Генерирует случайный токен."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    def _generate_test_image(self) -> Image.Image:
        """Создает тестовое изображение, если нет доступных файлов."""
        img = Image.new('RGB', (300, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Рисуем простой узор для теста
        for i in range(0, 300, 30):
            draw.line([(i, 0), (i, 300)], fill=(0, 0, 0), width=2)
            draw.line([(0, i), (300, i)], fill=(0, 0, 0), width=2)
        return img

    def _convert_to_rgb(self, img: Image.Image) -> Image.Image:
        """Конвертирует изображение в RGB с белым фоном."""
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, color=(255, 255, 255))
            bg.paste(img, mask=img.split()[3])
            return bg
        elif img.mode != 'RGB':
            return img.convert('RGB')
        return img

    def _image_to_base64(self, img: Image.Image) -> str:
        """Конвертирует PIL Image в base64 строку."""
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_str

    def _generate_grid_mode(self, token: str, image_filename: Optional[str] = None) -> dict:
        """Режим разрезания одного изображения на сетку."""
        if image_filename is None:
            if not self.image_files:
                img = self._generate_test_image()
            else:
                image_filename = random.choice(self.image_files)

        if image_filename:
            image_path = os.path.join(self.image_dir, image_filename)
            if os.path.exists(image_path):
                img = Image.open(image_path)
            else:
                img = self._generate_test_image()
        else:
            img = self._generate_test_image()

        if img.mode != 'RGB':
            img = img.convert('RGB')

        target_size = (300, 300)
        img = img.resize(target_size, Image.Resampling.LANCZOS)

        grid_size = 3
        fragment_size = img.width // grid_size

        fragments = []
        correct_order = []

        for row in range(grid_size):
            for col in range(grid_size):
                left = col * fragment_size
                top = row * fragment_size
                right = left + fragment_size
                bottom = top + fragment_size

                fragment = img.crop((left, top, right, bottom))
                fragment = self._convert_to_rgb(fragment)
                fragment_base64 = self._image_to_base64(fragment)
                fragments.append(fragment_base64)
                correct_order.append(row * grid_size + col)

        self.challenges[token] = {
            "correct_order": correct_order,
            "grid_size": grid_size,
            "image_filename": image_filename
        }

        return {
            "token": token,
            "fragments": fragments,
            "grid_size": grid_size,
            "correct_order": correct_order,
            "num_pieces": len(fragments),
            "reference_image": None,
            "shuffled_indices": list(range(len(fragments))),
        }

    def _generate_pieces_mode(self, token: str) -> dict:
        """Режим использования готовых фрагментов как кусков пазла."""
        if not self.image_files:
            raise ValueError("Нет изображений в директории image/")

        pieces = []
        for filename in self.image_files:
            image_path = os.path.join(self.image_dir, filename)
            if os.path.exists(image_path):
                img = Image.open(image_path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                pieces.append((filename, img))

        num_pieces = len(pieces)
        grid_size = 2 if num_pieces == 4 else int(num_pieces ** 0.5) or num_pieces

        reference_img = Image.new('RGB', (200 * grid_size, 200 * grid_size), color=(255, 255, 255))
        for idx, (filename, img) in enumerate(pieces):
            rgb_img = self._convert_to_rgb(img)
            row = idx // grid_size
            col = idx % grid_size
            reference_img.paste(rgb_img, box=(col * 200, row * 200))

        reference_base64 = self._image_to_base64(reference_img)

        indices = list(range(num_pieces))
        random.shuffle(indices)
        if indices == list(range(num_pieces)) and num_pieces > 1:
            indices[0], indices[1] = indices[1], indices[0]
        shuffled_indices = indices

        shuffled_pieces = [pieces[i] for i in shuffled_indices]

        self.challenges[token] = {
            "correct_order": list(range(num_pieces)),
            "grid_size": grid_size,
            "num_pieces": num_pieces,
            "shuffled_indices": shuffled_indices
        }

        fragments = []
        for filename, img in shuffled_pieces:
            rgb_img = self._convert_to_rgb(img)
            fragment_base64 = self._image_to_base64(rgb_img)
            fragments.append(fragment_base64)

        return {
            "token": token,
            "fragments": fragments,
            "grid_size": grid_size,
            "correct_order": list(range(num_pieces)),
            "num_pieces": num_pieces,
            "reference_image": reference_base64,
            "shuffled_indices": shuffled_indices,
        }

    def get_fragment_image(self, token: str, index: int) -> Optional[Image.Image]:
        """Возвращает фрагмент пазла как PIL Image по токену и индексу."""
        challenge = self.challenges.get(token)
        if not challenge:
            return None

        num_pieces = challenge.get("num_pieces", 0)
        if index < 0 or index >= num_pieces:
            return None

        image_path = os.path.join(self.image_dir, self.image_files[index])
        if not os.path.exists(image_path):
            return None

        img = Image.open(image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        return self._convert_to_rgb(img)

    def get_reference_image(self, token: str) -> Optional[Image.Image]:
        """Возвращает reference изображение (собранный пазл) как PIL Image."""
        challenge = self.challenges.get(token)
        if not challenge:
            return None

        num_pieces = challenge.get("num_pieces", 0)
        grid_size = challenge.get("grid_size", 2)

        if num_pieces == 0 or not self.image_files:
            return None

        reference_img = Image.new('RGB', (200 * grid_size, 200 * grid_size), color=(255, 255, 255))
        for idx in range(num_pieces):
            image_path = os.path.join(self.image_dir, self.image_files[idx])
            if os.path.exists(image_path):
                img = Image.open(image_path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                rgb_img = self._convert_to_rgb(img)
                row = idx // grid_size
                col = idx % grid_size
                reference_img.paste(rgb_img, box=(col * 200, row * 200))

        return reference_img

    def verify(self, token: str, fragment_order: list[int]) -> bool:
        """
        Проверяет правильность сборки пазла.

        fragment_order - последовательность оригинальных индексов
        в текущем порядке на сетке. Если пазл собран верно,
        fragment_order должен быть [0, 1, 2, ...].
        """
        challenge = self.challenges.get(token)
        if not challenge:
            return False

        correct_order = challenge.get("correct_order", [])
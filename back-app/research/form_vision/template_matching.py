import cv2
from typing import Tuple, Generator
from research.form_vision.image import Image, NormalizedCoords
import numpy as np


class TemplateMatcher:
    width = 800

    def __init__(
        self, template_image: Image, reference_region: Tuple[NormalizedCoords, NormalizedCoords]
    ):
        self._template = template_image.resize(self.width)
        self._reference_region = reference_region
        self._reference = self._template.select_subimage(*reference_region)
        self._ref_region_height = reference_region[1][0] - reference_region[0][0]
        self._ref_region_width = reference_region[1][1] - reference_region[0][1]

    def match(self, img: Image) -> Image:
        img = img.crop_to_aspect_ratio(self._template.aspect_ratio)
        img = img.resize(width=self.width)
        region_to_search_coords = self._around_reference_region()
        region_to_search = img.select_subimage(*region_to_search_coords)

        best_top_left, most_similar = None, 0.0
        for (scaled_rotated_img, scale_factor, angle) in self._get_scaled_rotated_versions(img):
            top_left, similarity = self._match_template(scaled_rotated_img)
            found_match = self._extract_match(region_to_search, top_left)
            return found_match
            if similarity > most_similar:
                most_similar = similarity
                best_top_left = top_left

        top_left, sim = self._match_template(region_to_search)
        found_match = self._extract_match(region_to_search, top_left)
        print(sim)
        return found_match

    def _around_reference_region(
        self, coeff: float = 0.5
    ) -> Tuple[NormalizedCoords, NormalizedCoords]:

        start_vert = max(0, self._reference_region[0][0] - self._ref_region_height * coeff / 2)
        start_horiz = max(0, self._reference_region[0][1] - self._ref_region_width * coeff / 2)
        end_vert = min(1, self._reference_region[1][0] + self._ref_region_height * coeff / 2)
        end_horiz = min(1, self._reference_region[1][1] + self._ref_region_width * coeff / 2)
        return ((start_vert, start_horiz), (end_vert, end_horiz))

    def _extract_match(self, searched_region: Image, top_left: NormalizedCoords) -> Image:
        return searched_region[
            top_left[0] : top_left[0] + int(self._ref_region_height * self._template.shape[0]),
            top_left[1] : top_left[1] + int(self._ref_region_width * self._template.shape[1]),
        ]

    def _get_scaled_rotated_versions(
        self, image: Image
    ) -> Generator[Tuple[Image, float, float], None, None]:
        for scaling_factor in np.arange(0.9, 1.1, 0.02):
            for angle in np.arange(-3, 3, 0.3):
                yield (
                    image.resize(int(scaling_factor * image.shape[1])).rotate(angle),
                    scaling_factor,
                    angle,
                )

    def _match_template(self, image_to_search: Image) -> Tuple[NormalizedCoords, float]:
        res = cv2.matchTemplate(
            image_to_search.image_data, self._reference.image_data, cv2.TM_CCOEFF
        )
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return max_loc[::-1], max_val

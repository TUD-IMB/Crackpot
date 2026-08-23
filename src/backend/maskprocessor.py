from skimage.measure import label, regionprops


class MaskProcessor:
	r"""
	Process crack prediction masks. Provides a function to remove small, disconnected
	mask patches that are likely segmentation noise rather than actual cracks.
	"""

	def remove_small_patches(self, mask, min_patch_area):
		r"""
		Remove small disconnected foreground regions from a crack mask.

		\param mask: The crack prediction mask. Nonzero pixels are treated as foreground.
		\param min_patch_area: The minimum area (in pixels) a connected region must have to be kept.
		\return: The cleaned mask with small patches removed.
		"""
		labeled_mask = label(mask > 0, connectivity=2)
		cleaned_mask = mask.copy()
		for region in regionprops(labeled_mask):
			if region.area < min_patch_area:
				rows, cols = region.coords[:, 0], region.coords[:, 1]
				cleaned_mask[rows, cols] = 0
		return cleaned_mask

export function floodFill(image, sr, sc, color) {
  const startColor = image[sr][sc];
  if (startColor === color) return image;

  const rows = image.length;
  const cols = image[0].length;
  const stack = [[sr, sc]];

  while (stack.length > 0) {
    const [r, c] = stack.pop();
    if (r < 0 || r >= rows || c < 0 || c >= cols) continue;
    if (image[r][c] !== startColor) continue;

    image[r][c] = color;
    stack.push([r + 1, c], [r - 1, c], [r, c + 1], [r, c - 1]);
  }

  return image;
}

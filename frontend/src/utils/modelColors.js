// Utility to assign consistent colors to models
const modelColorMap = new Map();
const colors = [0, 1, 2, 3, 4, 5]; // Available color schemes
let colorIndex = 0;

// Color palette for models
const colorPalette = [
  '#3B82F6', // Blue
  '#10B981', // Green
  '#F59E0B', // Amber
  '#EF4444', // Red
  '#8B5CF6', // Purple
  '#EC4899', // Pink
];

export function getModelColorClass(modelName) {
  if (!modelColorMap.has(modelName)) {
    modelColorMap.set(modelName, colors[colorIndex % colors.length]);
    colorIndex++;
  }
  return `model-color-${modelColorMap.get(modelName)}`;
}

export function getModelColor(modelName) {
  if (!modelColorMap.has(modelName)) {
    modelColorMap.set(modelName, colors[colorIndex % colors.length]);
    colorIndex++;
  }
  const index = modelColorMap.get(modelName);
  return colorPalette[index % colorPalette.length];
}

export function resetModelColors() {
  modelColorMap.clear();
  colorIndex = 0;
}

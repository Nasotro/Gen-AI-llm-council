// Utility to assign consistent colors to models
const modelColorMap = new Map();
const colors = [0, 1, 2, 3, 4, 5]; // Available color schemes
let colorIndex = 0;

export function getModelColorClass(modelName) {
  if (!modelColorMap.has(modelName)) {
    modelColorMap.set(modelName, colors[colorIndex % colors.length]);
    colorIndex++;
  }
  return `model-color-${modelColorMap.get(modelName)}`;
}

export function resetModelColors() {
  modelColorMap.clear();
  colorIndex = 0;
}

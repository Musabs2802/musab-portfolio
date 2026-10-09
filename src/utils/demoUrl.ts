// Resolve a sample dashboard path against the app's base URL
export const getDemoUrl = (demo: string) => {
  if (/^(https?:)?\/\//.test(demo)) {
    return demo;
  }

  const normalizedPath = demo.replace(/^\/+/, "");
  return `${import.meta.env.BASE_URL}${normalizedPath}`;
};

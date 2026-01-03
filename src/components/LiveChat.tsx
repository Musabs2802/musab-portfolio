import { useEffect } from "react";

export default function LiveChat() {
  useEffect(() => {
    const script = document.createElement("script");
    script.src = "https://embed.tawk.to/69593c6d56031d197dfe187e/1je2983cg";
    script.async = true;
    document.body.appendChild(script);
  }, []);

  return null;
}

// Contact details and links used across the site
const site = {
  name: "Musab Shaikh",
  email: "musabs2802@gmail.com",
  phone: "+966507055745",
  phoneDisplay: "+966 50 705 5745",
  whatsapp: "https://wa.me/966507055745",
  calendly: "https://calendly.com/musabs2802/introductory-meeting",
  linkedin: "https://www.linkedin.com/in/musab-shaikh-2802/",
  github: "https://github.com/Musabs2802",
  location: "Jeddah, Saudi Arabia",
  responseTime: "Replies within 24 hours",
  avatar:
    "https://res.cloudinary.com/de75b0zis/image/upload/v1767276493/musab-img_dbulfo.png",
  workingImage:
    "https://res.cloudinary.com/de75b0zis/image/upload/v1767276292/musab-working-img_pb9nkt.png",
};

export const whatsappLink = (message: string) =>
  `${site.whatsapp}?text=${encodeURIComponent(message)}`;

export default site;

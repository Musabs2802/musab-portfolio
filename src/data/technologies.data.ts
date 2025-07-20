import { siAirtable, siAndroid, siCloudflare, siFlutter, siIos, siJavascript, siMongodb, siNodedotjs, siPostgresql, siPython, siReact, siSqlite, siTypescript } from "simple-icons";
import { Technology } from "../types";

const technologiesData: Technology[] = [
    {name: 'Android', icon: siAndroid, category: 'Frontend'},
    {name:'iOS', icon: siIos, category: 'Frontend'},
    {name: 'Flutter', icon:siFlutter, category: 'Frontend'},
    { name: 'React', icon: siReact, category: 'Frontend' },
  { name: 'JavaScript', icon: siJavascript, category: 'Language' },
  { name: 'TypeScript', icon: siTypescript, category: 'Language' },
  { name: 'Node.js', icon: siNodedotjs, category: 'Backend' },
  { name: 'Python', icon: siPython, category: 'Language' },
  { name: 'SQL', icon: siSqlite, category: 'Database' },
  { name: 'PostgreSQL', icon: siPostgresql, category: 'Database' },
  { name: 'MongoDB', icon: siMongodb, category: 'Database' },
    {name: 'AWS', icon:siCloudflare, category: 'Backend'},
    {name: 'Excel', icon: siAirtable, category: 'Data'}
];

export default technologiesData
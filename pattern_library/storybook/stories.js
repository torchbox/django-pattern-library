import { storiesOf } from "@storybook/html";
import { renderPattern, simulateLoading } from "./storybook-django";

const generateStories = (prefix, group) => {
    let stored = [];
    if (group.templates_stored) {
        stored = group.templates_stored.map(template => ({
            label: template.pattern_name || template.pattern_filename,
            path: `${prefix}/${template.pattern_filename}`,
        }))
    }

    return stored.concat(...Object.entries(group.template_groups).map(([group_name, subgroup]) => {
        return generateStories(`${prefix}/${group_name}`, subgroup);
    }));
}

(async () => {
    const templates = await window.fetch("/api/v1/").then((res) => res.json());
    console.log(templates);
    const storyStore = window.__STORYBOOK_STORY_STORE__;

    storyStore.startConfiguring();
    Object.entries(templates.template_groups).forEach(([group_name, group_contents]) => {
        console.log(group_name);
        const stories = generateStories(group_name, group_contents);
        console.log(stories);
        const group = storiesOf(group_name);
        stories.forEach(story => {
            group.add(story.label, (args) => {
                const t = document.createElement("div");

                renderPattern(
                    `/render-pattern/patterns/${story.path}`,
                )
                    .catch((err) => simulateLoading(t, err))
                    .then((res) => res.text())
                    .then((html) => simulateLoading(t, html));

                return t;
            });
        });
    });
    storyStore.finishConfiguring();
})();

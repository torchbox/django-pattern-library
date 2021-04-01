const initAccordions = () => {
    const accordions = [...document.querySelectorAll("[data-accordion]")];
    accordions.forEach((node) => {
        const panels = [
            ...document.querySelectorAll("[data-accordion-panel]", node),
        ];

        panels.forEach((panel, i) => {
            const isFirst = i === 0;

            const toggle = panel.querySelector("[data-accordion-toggle]");
            const content = panel.querySelector("[data-accordion-content]");

            if (!toggle || !content) {
                return;
            }

            toggle.addEventListener("click", () => {
                const wasOpen = toggle.getAttribute("aria-pressed") === "true";
                const isOpen = !wasOpen;

                toggle.setAttribute("aria-pressed", isOpen);
                toggle.setAttribute("aria-expanded", isOpen);
                content.hidden = !isOpen;
            });

            // All panels are open by default. When JS kicks in, the first panel stays open,
            // other panels are closed.
            if (isFirst) {
                toggle.setAttribute("aria-pressed", true);
                toggle.setAttribute("aria-expanded", true);
                content.hidden = false;
            } else {
                toggle.setAttribute("aria-pressed", false);
                toggle.setAttribute("aria-expanded", false);
                content.hidden = true;
            }
        });
    });
};

document.addEventListener('DOMContentLoaded', () => {
    initAccordions();
});

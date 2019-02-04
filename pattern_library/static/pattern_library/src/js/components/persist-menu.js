export default function() {
    if (location.pathname.includes('/pattern/')) {
        // split url to match {{ template.origin.template_name }}
        const id = location.pathname.split('/pattern/')[1];

        // find the matching pattern
        const currentPattern = document.getElementById(id);

        currentPattern.classList.add('is-active');

        // grab the parent lists and headings
        const parentCategory = currentPattern.closest('ul');
        const parentCategoryHeading = parentCategory.previousElementSibling;
        const grandParentCategory = parentCategoryHeading.closest('ul');
        const grandParentCategoryHeading = grandParentCategory.previousElementSibling;

        parentCategory.classList.add('is-open');
        parentCategoryHeading.classList.add('is-open');
        grandParentCategory.classList.add('is-open');
        grandParentCategoryHeading.classList.add('is-open');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const languageSelect = document.getElementById('language');

    function updateFlag() {
        const selectedOption = languageSelect.options[languageSelect.selectedIndex];
        const flagUrl = selectedOption.getAttribute('data-flag');
        languageSelect.style.backgroundImage = `url(${flagUrl})`;

        for (let i = 0; i < languageSelect.options.length; i++) {
            const option = languageSelect.options[i];
            const optionFlagUrl = option.getAttribute('data-flag');
            option.style.backgroundImage = `url(${optionFlagUrl})`;
            option.style.backgroundRepeat = 'no-repeat';
            option.style.backgroundPosition = '5px center';
        }
    }

    updateFlag();

    languageSelect.addEventListener('change', updateFlag);
});
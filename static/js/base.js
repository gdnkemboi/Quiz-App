let currentCardIndex = 0;
const cards = document.querySelectorAll('.question');

function showCard(index) {
  cards.forEach(card => card.style.display = 'none');
  cards[index].style.display = 'flex';
}

function nextCard() {
  if (currentCardIndex < cards.length - 1) {
    currentCardIndex++;
    showCard(currentCardIndex);
  }
}

function prevCard() {
  if (currentCardIndex > 0) {
    currentCardIndex--;
    showCard(currentCardIndex);
  }
}

showCard(currentCardIndex);

function selectRadioButton(liElement) {
  var radioButton = liElement.querySelector('input[type="radio"]');
  if (radioButton) {
    radioButton.click();
  }
  let prevSelectedLi = document.querySelector('.selected');
  if (prevSelectedLi) {
    prevSelectedLi.classList.remove('selected');
  }

  liElement.classList.add('selected');
}

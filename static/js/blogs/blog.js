const copyUrl = () => {
  const url = window.location.href;
  navigator.clipboard.writeText(url)
  .then(() => {
    alert('URL copied to clipboard');
  }).catch(err => {
    alert('Failed to copy: ', err);
  });
}

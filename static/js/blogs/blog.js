const copyUrl = () => {
  const url = window.location.href;
  const copyBtn = document.getElementById("copyBtn");
  navigator.clipboard.writeText(url)
  .then(() => {
    const popover = new bootstrap.Popover(copyBtn, {
      content: 'URL copied to clipboard',
      trigger: 'manual'
    });
    popover.show();
    setTimeout(() => popover.hide(), 2000); // Hide the popover after 2 seconds
  }).catch(err => {
    const popover = new bootstrap.Popover(copyBtn, {
      content: 'Failed to copy: ' + err,
      trigger: 'manual'
    });
    popover.show();
    setTimeout(() => popover.hide(), 2000); // Hide the popover after 2 seconds
  });
}

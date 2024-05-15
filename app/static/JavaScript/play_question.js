function timeSince(_, dateposted) {
    let date = new Date(dateposted.getAttribute('dateposted'));
    let seconds = Math.floor((new Date() - date) / 1000) + date.getTimezoneOffset() * 60;
    let interval = seconds / 31536000;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " years ago";
        return;
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " months ago";
        return ;
    }
    interval = seconds / 86400;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) +" days ago";
        return;
    }
    interval = seconds / 3600;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " hours ago";
        return;
    }
    interval = seconds / 60;
    if (interval > 1) {
        dateposted.innerText = Math.floor(interval) + " minutes ago";
        return;
    }
    dateposted.innerText = Math.floor(interval) + " seconds";
}

function setTimes() {
    $('.dateposted').each(timeSince)
}

$(document).ready(function () {
    setTimes();
    setInterval(setTimes, 5000)
})

document.addEventListener("DOMContentLoaded", function () {
  // By using the same script.js file for all pages, we can avoid
  // duplicating code.  However, we need to check if the element
  // exists before using it.  For example, the new-post-form only
  // exists on the index page, so we need to check if it exists
  // before using it.
  const newPostForm = document.querySelector('#new-post-form');
  if (newPostForm) {
    newPostForm.onsubmit = function () {
      const text = document.querySelector('#new-post-text').value
      // Trim the text to remove whitespace at the beginning and end. If
      // the text is empty, alert the user and prevent the form from
      // being submitted.
      if (text.trim().length === 0) {
        alert('Post text is empty!');
        return false;
      }
      // Fetch the CSRF token from the hidden input field
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      // Send a POST request to the /posts route with the text of the
      // post in the body. Then, reload the page.
      fetch('/network/posts', {
        method: 'POST',
        body: JSON.stringify({
          text: document.querySelector('#new-post-text').value
        }),
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
        .then(response => response.json())
        .then(result => {
          if (result.error) {
            alert(result.error);
          } else {
            window.location.reload();
          }
        }).catch(() => {
          alert('Something went wrong!');
        });
      return false;
    }
  }

  // Like button functionality
  document.querySelectorAll('.like-button').forEach(button => {
    button.onclick = function () {
      // Fetch the CSRF token from the hidden input field
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      // Get the post_id from the data-post_id attribute
      const post_id = button.dataset.post_id;
      const like_count = document.querySelector(`#like-count-${post_id}`);
      // Send a PUT request to the /like route with the post_id in the
      // URL. Then, update the like count and the color of the button.
      fetch(`/network/like/${post_id}`, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
        .then(response => response.json())
        .then(result => {
          if (result.error) {
            alert(result.error);
          } else {
            like_count.innerHTML = result.likes;
            if (result.liked) {
              button.classList.add('text-danger');
            } else {
              button.classList.remove('text-danger');
            }
          }
        });
    }
  })

  // Edit post functionality (Bootstrap modal)
  document.querySelectorAll('.edit-post-form').forEach(form => {
    form.onsubmit = function (event) {
      // Prevent the form from being submitted
      event.preventDefault();
      // Get the post_id from the data-post_id attribute and the text
      // from the form field
      const post_id = form.dataset.post_id;
      const text = document.querySelector(`#edit-text-${post_id}`).value;
      // Fetch the CSRF token from the hidden input field
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      // Send a PUT request to the /posts/<post_id> route with the text
      // in the body. Then, update the post text and hide the modal.
      fetch(`/network/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          text: text
        }),
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
        .then(response => response.json())
        .then(result => {
          if (result.error) {
            alert(result.error);
          } else {
            // Update the post text
            document.querySelector(`#post-text-${post_id}`).innerHTML = text;
            // Hide the modal
            const container = document.querySelector(`#edit-post-modal-${post_id}`);
            const modal = bootstrap.Modal.getInstance(container);
            modal.hide();
          }
        })
        .catch(() => {
          alert('Something went wrong!');
        });
      return false;
    }
  })

  // Follow button functionality
  const followButton = document.querySelector('#follow-button');
  if (followButton) {
    // Get the user_id from the data-user_id attribute
    document.querySelector('#follow-button').onclick = function () {
      // Fetch the CSRF token from the hidden input field
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const user_id = document.querySelector('#follow-button').dataset.user_id;
      // Send a PUT request to the /follow/<user_id> route. Then, reload
      // the page.
      fetch(`/network/follow/${user_id}`, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': csrftoken
        }
      })
        .then(response => response.json())
        .then(result => {
          if (result.error) {
            alert(result.error);
          } else {
            window.location.reload();
          }
        })
        .catch(() => {
          alert('Something went wrong!');
        });
    }
  }
});



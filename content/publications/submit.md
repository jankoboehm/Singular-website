---
title: "Give Notice of a Publication"
url: "/publications/submit/"
description: "Submit a Singular-related publication notice for review."
section_label: "Publication database"
migration_status: "new functional replacement for the legacy publication notice form"
---

Use this form to give notice of a publication related to Singular. The fields and publication categories match the legacy submission form so existing publication information can continue to be collected without changing meaning.

<form class="publication-submit-form" action="/publications/submit/notice.php" method="post" enctype="multipart/form-data" accept-charset="utf-8">
  <fieldset>
    <legend>Authors</legend>
    <div class="form-grid form-grid--authors">
      <label>Author 1 first name <input type="text" name="author1firstname" autocomplete="given-name"></label>
      <label>Author 1 surname <input type="text" name="author1surname" autocomplete="family-name" required></label>
      <label>Author 2 first name <input type="text" name="author2firstname"></label>
      <label>Author 2 surname <input type="text" name="author2surname"></label>
      <label>Author 3 first name <input type="text" name="author3firstname"></label>
      <label>Author 3 surname <input type="text" name="author3surname"></label>
      <label>Author 4 first name <input type="text" name="author4firstname"></label>
      <label>Author 4 surname <input type="text" name="author4surname"></label>
      <label>Author 5 first name <input type="text" name="author5firstname"></label>
      <label>Author 5 surname <input type="text" name="author5surname"></label>
      <label>Author 6 first name <input type="text" name="author6firstname"></label>
      <label>Author 6 surname <input type="text" name="author6surname"></label>
    </div>
  </fieldset>

  <fieldset>
    <legend>Publication</legend>
    <div class="form-grid">
      <label class="full">Title <input type="text" name="title" required></label>
      <label>Journal/Publisher <input type="text" name="journal"></label>
      <label>Volume <input type="text" name="volume"></label>
      <label>Pages <input type="text" name="pages"></label>
      <label>Year <input type="text" name="year" inputmode="numeric"></label>
      <label class="full">Extras <input type="text" name="extra" placeholder="e.g. 2nd edition 2007"></label>
      <label class="full">Link <input type="url" name="link" placeholder="https://"></label>
      <label class="full">Type
        <select name="type">
          <option selected value="0">publication referring to Singular</option>
          <option value="1">publication providing Singular examples</option>
          <option value="2">publication providing implemented algorithms</option>
          <option value="3">Singular manual / tutorial</option>
          <option value="4">overview articles</option>
          <option value="5">introductory textbooks</option>
          <option value="6">Singular presentation</option>
        </select>
      </label>
    </div>
  </fieldset>

  <label class="honeypot">Website <input type="text" name="website" autocomplete="off" tabindex="-1"></label>
  <button class="button" type="submit">Submit publication notice</button>
</form>

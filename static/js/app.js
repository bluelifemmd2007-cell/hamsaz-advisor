(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initLocationPicker();
    initCustomFieldsToggle();
    initRadioCardHighlight();
  });

  function initLocationPicker() {
    var select = document.getElementById("location-select");
    var searchInput = document.getElementById("location-search");
    var resultsBox = document.getElementById("location-results");
    var hint = document.getElementById("selected-location-hint");

    if (!select || !searchInput || !resultsBox) {
      return; // Not on a page that has the picker - nothing to do.
    }

   
    var entries = [];
    Array.prototype.forEach.call(select.children, function (child) {
      if (child.tagName === "OPTGROUP") {
        Array.prototype.forEach.call(child.children, function (opt) {
          entries.push({ value: opt.value, label: opt.textContent, group: child.label });
        });
      }
    });

    function currentLabel() {
      var opt = select.options[select.selectedIndex];
      return opt ? opt.textContent : "";
    }

    function updateHint() {
      if (!hint) return;
      if (select.value && select.value !== "custom" && select.value !== "") {
        hint.textContent = "Selected: " + currentLabel();
      } else {
        hint.textContent = "";
      }
    }

    function renderResults(query) {
      var q = query.trim().toLowerCase();
      resultsBox.innerHTML = "";

      if (q.length === 0) {
        resultsBox.hidden = true;
        return;
      }

      var matches = entries.filter(function (entry) {
        return (
          entry.label.toLowerCase().indexOf(q) !== -1 ||
          entry.group.toLowerCase().indexOf(q) !== -1
        );
      });

      if (matches.length === 0) {
        var empty = document.createElement("div");
        empty.className = "location-empty";
        empty.textContent = "No matching city - try 'Custom location' below the list.";
        resultsBox.appendChild(empty);
        resultsBox.hidden = false;
        return;
      }

      var lastGroup = null;
      matches.slice(0, 60).forEach(function (entry) {
        if (entry.group !== lastGroup) {
          var groupLabel = document.createElement("div");
          groupLabel.className = "location-group-label";
          groupLabel.textContent = entry.group;
          resultsBox.appendChild(groupLabel);
          lastGroup = entry.group;
        }
        var btn = document.createElement("button");
        btn.type = "button";
        btn.className = "location-option";
        btn.textContent = entry.label;
        btn.addEventListener("click", function () {
          select.value = entry.value;
          searchInput.value = entry.label;
          resultsBox.hidden = true;
          updateHint();
          select.dispatchEvent(new Event("change"));
        });
        resultsBox.appendChild(btn);
      });

      resultsBox.hidden = false;
    }

    searchInput.addEventListener("input", function () {
      renderResults(searchInput.value);
    });

    searchInput.addEventListener("focus", function () {
      if (searchInput.value.trim().length > 0) {
        renderResults(searchInput.value);
      }
    });

    document.addEventListener("click", function (event) {
      var picker = document.querySelector(".location-picker");
      if (picker && !picker.contains(event.target)) {
        resultsBox.hidden = true;
      }
    });

    select.classList.add("js-hidden");

    if (select.value && select.value !== "custom") {
      searchInput.value = currentLabel();
    }
    updateHint();
  }

  function initCustomFieldsToggle() {
    var select = document.getElementById("location-select");
    var customFields = document.getElementById("custom-fields");
    if (!select || !customFields) return;

    function sync() {
      customFields.hidden = select.value !== "custom";
    }

    select.addEventListener("change", sync);
    sync();
  }

  function initRadioCardHighlight() {
    var cards = document.querySelectorAll(".radio-card");
    if (!cards.length) return;

    cards.forEach(function (card) {
      var input = card.querySelector("input[type='radio']");
      if (!input) return;

      function sync() {
        var groupName = input.name;
        document.querySelectorAll("input[name='" + groupName + "']").forEach(function (radio) {
          var parent = radio.closest(".radio-card");
          if (!parent) return;
          parent.classList.toggle("checked", radio.checked);
        });
      }

      input.addEventListener("change", sync);
      sync();
    });
  }
})();

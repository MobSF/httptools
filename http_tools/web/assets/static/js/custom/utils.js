function html_encode(data) {
      return data
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#x27;")
      .replace(/`/g, "&#x60;")
      .replace(/\(/g, "&#x28;")
      .replace(/\)/g, "&#x29;")
      .replace(/{/g, "&#x7B;")
      .replace(/}/g, "&#x7D;")
      .replace(/-/g, "&#x2D;")
      .replace(/\+/g, "&#x2B;");

    }
define([
  'codemirror/lib/codemirror',
  'base/js/namespace',
], function(
  CodeMirror,
  IPython) {
    "use strict";
    var onload = function() {
        console.log("Loading kernel.js for SC_Kernel")
        enableSCMode(CodeMirror);
        IPython.CodeCell.options_default["cm_config"]["mode"] = "sclang";
        IPython.CodeCell.options_default['cm_config']['indentUnit'] = 2;
        var cells = IPython.notebook.get_cells();
        for (var i in cells){
            var c = cells[i];
            if (c.cell_type === 'code')
                c.code_mirror.setOption('indentUnit', 2);
        }
    }
    return {onload:onload};
});

var enableSCMode = function (CodeMirror) {
  CodeMirror.defineMode('sclang', function (config) {
    var keywords = ["arg", "classvar", "const", "super", "this", "var"];
    var builtIns = ["false", "inf", "nil", "true", "thisFunction", "thisFunctionDef", "thisMethod", "thisProcess", "thisThread", "currentEnvironment", "topEnvironment"];

    function consumeString(stream, state) {
      var curr_char;
      while(curr_char = stream.next()) {
        if (curr_char === "\\") {
          curr_char = stream.next();
        } else if (curr_char === "\"") {
          state.state = 0;
          return;
        };
      }
      // End of the line but must be still in a string
      return;
    };

    function consumeComment(stream, state) {
      var curr_char;
      var asterisk = false;
      while(curr_char = stream.next()) {
        console.log(curr_char);
        if (curr_char === "*") {
          asterisk = true;
        } else if (asterisk && curr_char === "\/") {
          state.commentLevel -= 1;
          if (state.commentLevel == 0) {
            state.state = 0;
            return;
          }
          asterisk = false;
        } else {
          asterisk = false;
        }
      };

      // End of line
      return;
    };

    function tokenize(stream, state) {
      // Inline Comments with //
      if (stream.match(/^\/\//)) {
        stream.skipToEnd();
        return "comment";
      };

      // Multiline comments
      if (stream.match(/^\/\*/)) {
        state.state = 2;
        state.commentLevel += 1;
        consumeComment(stream, state);
        return "comment";
      };

      // Symbol
      if (stream.match(/^\'/)) {
        var curr_char;
        while (curr_char = stream.next()) {
          if (curr_char === "\\") {
            // consume next character because it will be ignored
            curr_char = stream.next();
          } else if (curr_char === "'") {
            return "string"
          };
        }

        // Only get here if it is the end of a line
        return "string";
      };

      // Symbol with a slash
      if (stream.match(/^\\\w*/)) {
        return "string";
      };

      // Strings
      if (stream.match(/^\"/)) {
        state.state = 1;
        consumeString(stream, state);
        return "string";
      };

      // White space
      if (stream.eatSpace()) {
        return null;
      };

      // Radix float
      if (stream.match(/^[0-9]+r[0-9a-zA-Z]*(\.[0-9A-Z]*)?/)) {
        return "number";
      };

      // Scale degrees
      if (stream.match(/^\d+(s+|b+|[sb]\d+)/)) {
        return "number"
      };

      // Hex Float
      if (stream.match(/^0x(\d|[a-f]|[A-F])+/)) {
        return "number"
      };

      // Floats
      if (stream.match(/^(pi)|[0-9]+(\.[0-9]+)?([eE][\-\+]?[0-9]+)?(pi)?/)) {
        return "number";
      };

      // Symbol args
      if (stream.match(/^[a-zA-Z]+[:]/)) {
        return "builtin"
      }

      // Primitive
      if (stream.match(/^[_][a-zA-Z]/)) {
        return "atom";
      }

      // Char
      if (stream.match(/^\$\\?./)) {
        return "string";
      }

      // Environment variable
      if (stream.match(/^\~[a-z]\w*/)) {
        return "variable-3";
      }

      // Class name
      if(stream.match(/^[A-Z]\w*/)) {
        return "atom";
      };

      // Builtins, keywords, variable names
      // Needs to be after primitive because this captures _
      var m;
      if(m = stream.match(/^\w+/)) {
        var word = m[0];
        if (builtIns.indexOf(word) > -1) {
          return "builtin";
        } else if(keywords.indexOf(word) > -1) {
          return "keyword";
        } else {
          return "variable-2";
        };
      };

      // If we can't match anything then consume and move to next char
      stream.next();
      return null;
    };

    // States
    // 0 : normal
    // 1 : inString
    // 2 : inComment
    return {
      startState: function startState() {
        return {
          state: 0,
          commentLevel: 0
        }
      },
      token: function(stream, state) {
        var token_name;
        if (state.state == 0 ) {
          token_name = tokenize(stream, state);
        } else if (state.state == 1) {
          consumeString(stream, state);
          token_name = "string";
        } else if (state.state == 2) {
          consumeComment(stream, state);
          token_name = "comment";
        }
        return token_name;
      }
    }
  });
};

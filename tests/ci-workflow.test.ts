import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const workflow = readFileSync(".github/workflows/ci.yml", "utf8");

describe("ci workflow", () => {
  it("assembles the public Clerk build placeholder so no key-shaped literal is committed", () => {
    const publicPlaceholder =
      "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: " +
      "${{ format('pk_test_{0}', 'Y2xlcmsuZXhhbXBsZS5jb20k') }}";

    expect(workflow).toContain(publicPlaceholder);
    // A raw pk_test_ literal is what the full-history secret scan reports (GR-001/GR-002).
    expect(workflow).not.toContain("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: pk_test_");
  });
});
